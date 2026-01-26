import { BetterAuth } from "better-auth";

export const auth = BetterAuth({
  emailAndPassword: {
    enabled: true,
  },
  jwt: {
    secret: process.env.NEXT_PUBLIC_BETTER_AUTH_SECRET || "fallback-secret-for-dev",
  },
});

// Utility function to make authenticated requests
export const makeAuthenticatedRequest = async (
  url: string,
  options: RequestInit = {}
): Promise<Response> => {
  // Get the token from wherever it's stored (localStorage, cookies, etc.)
  const token = localStorage.getItem("auth-token"); // or however you store the token

  if (!token) {
    throw new Error("No authentication token found");
  }

  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
};

// Utility to save token after login
export const saveAuthToken = (token: string): void => {
  localStorage.setItem("auth-token", token);
};

// Utility to clear token on logout
export const clearAuthToken = (): void => {
  localStorage.removeItem("auth-token");
};

// Utility to get current token
export const getCurrentToken = (): string | null => {
  return localStorage.getItem("auth-token");
};