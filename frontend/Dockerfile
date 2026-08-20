FROM node:20-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app/dist /usr/share/caddy

EXPOSE 80
CMD ["sh", "-c", "printf 'window.__RUTAMAR_CONFIG__ = { apiUrl: \\\"%s\\\" };' \"${VITE_API_URL:-}\" > /usr/share/caddy/runtime-config.js && exec caddy run --config /etc/caddy/Caddyfile --adapter caddyfile"]
