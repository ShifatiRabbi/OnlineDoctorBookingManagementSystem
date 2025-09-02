FROM node:20-alpine
WORKDIR /app

# install first for better caching
COPY frontend/package*.json ./
RUN npm install

# copy the rest
COPY frontend /app

ENV NEXT_TELEMETRY_DISABLED=1
# Needed for reliable file watching on Windows bind mounts
ENV CHOKIDAR_USEPOLLING=true

EXPOSE 3000
CMD ["npm","run","dev","--","-p","3000","-H","0.0.0.0"]
