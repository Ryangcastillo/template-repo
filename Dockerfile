# Generic Dockerfile - adapt for your language and application
# This is a multi-stage example that can be customized

# Build stage (example for Node.js - adapt as needed)
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# For Python:
# FROM python:3.11-slim AS builder
# WORKDIR /app
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# For Go:
# FROM golang:1.21-alpine AS builder
# WORKDIR /app
# COPY go.mod go.sum ./
# RUN go mod download

# Runtime stage
FROM node:18-alpine
WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /app/node_modules ./node_modules

# Copy application code
COPY . .

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Change ownership and switch to non-root user
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port (adapt as needed)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/healthz || exit 1

# Start the application
CMD ["npm", "start"]