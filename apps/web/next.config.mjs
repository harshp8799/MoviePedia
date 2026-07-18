/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Allow importing the shared workspace packages (they ship untranspiled ESM JS).
  transpilePackages: [
    '@moviepedia/api-client',
    '@moviepedia/shared-config',
    '@moviepedia/shared-utils',
    '@moviepedia/design-tokens',
  ],
  images: {
    // Remote poster/backdrop hosts added in Phase 3/5 when the storage domain is known.
    remotePatterns: [],
  },
};

export default nextConfig;
