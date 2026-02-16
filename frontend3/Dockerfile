# Use Node.js LTS as base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml* ./

# Install pnpm globally
RUN npm install -g pnpm

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy application code
COPY . .

# Set port environment variable before build
ENV PORT=3001
ENV NITRO_PORT=3001

# Build the application
RUN pnpm run build

# Expose port
EXPOSE 3001

# Start the application
CMD ["node", ".output/server/index.mjs"]