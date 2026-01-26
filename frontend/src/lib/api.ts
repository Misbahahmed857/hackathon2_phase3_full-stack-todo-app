// Frontend utility for attaching JWT to API requests

export const makeAuthenticatedRequest = async (
  url: string,
  options: RequestInit = {}
): Promise<Response> => {
  // Get the token from localStorage (or however you store the token)
  const token = localStorage.getItem("auth-token");

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

// Generic GET request with auth
export const getWithAuth = async (url: string): Promise<any> => {
  const response = await makeAuthenticatedRequest(url, {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
};

// Generic POST request with auth
export const postWithAuth = async (url: string, data: any): Promise<any> => {
  const response = await makeAuthenticatedRequest(url, {
    method: "POST",
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
};

// Generic PUT request with auth
export const putWithAuth = async (url: string, data: any): Promise<any> => {
  const response = await makeAuthenticatedRequest(url, {
    method: "PUT",
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
};

// Generic DELETE request with auth
export const deleteWithAuth = async (url: string): Promise<any> => {
  const response = await makeAuthenticatedRequest(url, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
};