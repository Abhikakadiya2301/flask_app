# Use the official Nginx image from the Docker Hub
FROM nginx:alpine

# Copy the static files to the Nginx HTML directory
WORKDIR /usr/share/nginx/html
COPY . /usr/share/nginx/html/
# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
