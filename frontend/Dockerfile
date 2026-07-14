FROM node:20-alpine

# Set non-root user context for security (node user is pre-created in the image)
USER node

# Set the working directory
WORKDIR /app

# The following lines are commented out as placeholders, 
# but they represent the correct best-practice order for layer caching:
# COPY --chown=node:node package*.json ./
# RUN npm ci

# Copy the rest of the application code
# COPY --chown=node:node . .

# Expose the Vite dev server port
EXPOSE 5173

# Start development server
CMD ["npm", "run", "dev", "--", "--host"]
