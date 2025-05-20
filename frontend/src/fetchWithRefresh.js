// api/fetchWithRefresh.js
const refreshAccessToken = async () => {
  const res = await fetch("http://localhost:8000/api/token/refresh/", {
    method: "POST",
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("Refresh token expired");
  }
};

export const fetchWithRefresh = async (url, options = {}) => {
  let res = await fetch(url, {
    ...options,
    credentials: "include", // Required for cookies
  });

  if (res.status === 401) {
    try {
      await refreshAccessToken();

      // Retry original request after refresh
      res = await fetch(url, {
        ...options,
        credentials: "include",
      });
    } catch (err) {
      console.error("Refresh failed:", err);
      throw new Error("Unauthorized. Please login again.");
    }
  }

  return res;
};
