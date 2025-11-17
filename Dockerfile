# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with frozen lockfile
RUN npm ci --prefer-offline --no-audit

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy built application from builder
COPY --frombuilder --chownnextjs:nodejs /app/.next ./.next
COPY --frombuilder --chownnextjs:nodejs /app/package.json /app/package-lock.json ./
COPY --frombuilder --chownnextjs:nodejs /app/public ./public
COPY --frombuilder --chownnextjs:nodejs /app/node_modules ./node_modules

# Switch to non-root user
USER nextjs

EXPOSE 3000

# Add runtime configuration
ENV NEXT_TELEMETRY_DISABLED1
ENV NODE_ENVproduction

HEALTHCHECK --interval30s --timeout3s --start-period5s --retries3 \
  CMD node -e "require('http').get('http://localhost:3000', (r)  {if (r.statusCode ! 200) throw new Error(r.statusCode)})"

CMD ["npm", "start"]
