/**
 * Frontend Authentication Helper
 * 
 * This file provides helper functions and examples for managing authentication
 * in your frontend application (React, Vue, vanilla JS, etc.)
 */

// =============================================================================
// AUTHENTICATION API HELPER
// =============================================================================

class AuthAPI {
    constructor(baseURL = 'http://127.0.0.1:8000') {
        this.baseURL = baseURL;
    }

    // Helper method for making authenticated requests
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const config = {
            credentials: 'include', // IMPORTANT: Include cookies
            headers: {
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:5173',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            return {
                success: response.ok,
                status: response.status,
                data: data
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    // Login method
    async login(username, password) {
        return await this.request('/auth/login/', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    }

    // Logout method
    async logout() {
        return await this.request('/auth/logout/', {
            method: 'POST'
        });
    }

    // Check authentication status
    async checkAuth() {
        return await this.request('/auth/check-auth/', {
            method: 'GET'
        });
    }

    // Get user profile
    async getProfile() {
        return await this.request('/auth/profile/', {
            method: 'GET'
        });
    }

    // Register new user
    async register(userData) {
        return await this.request('/auth/register/', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }
}

// =============================================================================
// AUTHENTICATION STATE MANAGER
// =============================================================================

class AuthStateManager {
    constructor() {
        this.api = new AuthAPI();
        this.currentUser = null;
        this.isAuthenticated = false;
        this.listeners = [];
    }

    // Subscribe to authentication state changes
    subscribe(callback) {
        this.listeners.push(callback);
        return () => {
            this.listeners = this.listeners.filter(listener => listener !== callback);
        };
    }

    // Notify all listeners about state change
    notifyListeners() {
        this.listeners.forEach(callback => callback({
            isAuthenticated: this.isAuthenticated,
            user: this.currentUser
        }));
    }

    // Initialize authentication state
    async init() {
        const result = await this.api.checkAuth();
        
        if (result.success && result.data.is_authenticated) {
            this.currentUser = result.data;
            this.isAuthenticated = true;
        } else {
            this.currentUser = null;
            this.isAuthenticated = false;
        }
        
        this.notifyListeners();
        return this.isAuthenticated;
    }

    // Login
    async login(username, password) {
        const result = await this.api.login(username, password);
        
        if (result.success) {
            this.currentUser = result.data;
            this.isAuthenticated = true;
            this.notifyListeners();
            return { success: true, user: result.data };
        } else {
            this.currentUser = null;
            this.isAuthenticated = false;
            this.notifyListeners();
            return { success: false, error: result.data.error };
        }
    }

    // Logout
    async logout() {
        const result = await this.api.logout();
        
        // Clear state regardless of API response
        this.currentUser = null;
        this.isAuthenticated = false;
        this.notifyListeners();
        
        return result;
    }

    // Get current user
    getCurrentUser() {
        return this.currentUser;
    }

    // Check if user is authenticated
    isUserAuthenticated() {
        return this.isAuthenticated;
    }
}

// =============================================================================
// ROUTE PROTECTION HELPER
// =============================================================================

class RouteProtection {
    constructor(authManager) {
        this.authManager = authManager;
    }

    // Check if route requires authentication
    requiresAuth(route) {
        const protectedRoutes = [
            '/sell',
            '/profile',
            '/my-products',
            '/dashboard'
        ];
        
        return protectedRoutes.some(protectedRoute => 
            route.startsWith(protectedRoute)
        );
    }

    // Check if user can access route
    canAccess(route) {
        if (this.requiresAuth(route)) {
            return this.authManager.isUserAuthenticated();
        }
        return true;
    }

    // Get redirect URL for unauthorized access
    getRedirectUrl(route) {
        if (this.requiresAuth(route) && !this.authManager.isUserAuthenticated()) {
            return '/login';
        }
        return null;
    }
}

// =============================================================================
// USAGE EXAMPLES
// =============================================================================

// Example 1: Basic setup
const authManager = new AuthStateManager();
const routeProtection = new RouteProtection(authManager);

// Initialize authentication on app start
authManager.init();

// Example 2: Login form handler
async function handleLogin(username, password) {
    const result = await authManager.login(username, password);
    
    if (result.success) {
        console.log('Login successful!', result.user);
        // Redirect to dashboard or update UI
        window.location.href = '/dashboard';
    } else {
        console.error('Login failed:', result.error);
        // Show error message to user
        alert(result.error);
    }
}

// Example 3: Logout handler
async function handleLogout() {
    const result = await authManager.logout();
    console.log('Logged out');
    // Redirect to home page
    window.location.href = '/';
}

// Example 4: Route protection middleware
function protectRoute(route) {
    if (!routeProtection.canAccess(route)) {
        const redirectUrl = routeProtection.getRedirectUrl(route);
        if (redirectUrl) {
            window.location.href = redirectUrl;
            return false;
        }
    }
    return true;
}

// Example 5: React component example
/*
function App() {
    const [authState, setAuthState] = useState({
        isAuthenticated: false,
        user: null
    });

    useEffect(() => {
        // Initialize auth and subscribe to changes
        const unsubscribe = authManager.subscribe(setAuthState);
        authManager.init();
        
        return unsubscribe;
    }, []);

    const handleLogin = async (username, password) => {
        const result = await authManager.login(username, password);
        if (!result.success) {
            alert(result.error);
        }
    };

    const handleLogout = async () => {
        await authManager.logout();
    };

    return (
        <div>
            {authState.isAuthenticated ? (
                <div>
                    <h1>Welcome, {authState.user.username}!</h1>
                    <button onClick={handleLogout}>Logout</button>
                    <NavLink to="/profile">Profile</NavLink>
                    <NavLink to="/sell">Sell Product</NavLink>
                </div>
            ) : (
                <div>
                    <LoginForm onLogin={handleLogin} />
                </div>
            )}
        </div>
    );
}
*/

// Example 6: Vue.js composition API example
/*
import { ref, onMounted } from 'vue';

export default {
    setup() {
        const authState = ref({
            isAuthenticated: false,
            user: null
        });

        onMounted(() => {
            const unsubscribe = authManager.subscribe((state) => {
                authState.value = state;
            });
            authManager.init();
            
            onUnmounted(() => {
                unsubscribe();
            });
        });

        const login = async (username, password) => {
            const result = await authManager.login(username, password);
            if (!result.success) {
                alert(result.error);
            }
        };

        const logout = async () => {
            await authManager.logout();
        };

        return {
            authState,
            login,
            logout
        };
    }
};
*/

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AuthAPI,
        AuthStateManager,
        RouteProtection
    };
}

// Example 7: Navigation component logic
function updateNavigation() {
    const authState = authManager.isUserAuthenticated();
    const user = authManager.getCurrentUser();
    
    // Get navigation elements
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    const profileLink = document.getElementById('profile-link');
    const sellLink = document.getElementById('sell-link');
    const userGreeting = document.getElementById('user-greeting');
    
    if (authState) {
        // User is logged in
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'block';
        if (profileLink) profileLink.style.display = 'block';
        if (sellLink) sellLink.style.display = 'block';
        if (userGreeting) userGreeting.textContent = `Welcome, ${user.username}!`;
    } else {
        // User is not logged in
        if (loginLink) loginLink.style.display = 'block';
        if (logoutLink) logoutLink.style.display = 'none';
        if (profileLink) profileLink.style.display = 'none';
        if (sellLink) sellLink.style.display = 'none';
        if (userGreeting) userGreeting.textContent = '';
    }
}

// Subscribe to auth state changes to update navigation
authManager.subscribe(updateNavigation);

console.log('Authentication helper loaded. Available classes:', {
    AuthAPI,
    AuthStateManager,
    RouteProtection
});
