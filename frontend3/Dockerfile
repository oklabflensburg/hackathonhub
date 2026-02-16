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

# Build the application
RUN pnpm run build

# Expose port
EXPOSE 3001

# Set port environment variable
ENV PORT=3001
ENV NITRO_PORT=3001

# Start the application
CMD ["pnpm", "run", "preview"]