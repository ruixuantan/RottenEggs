FROM oven/bun AS builder

WORKDIR /app

COPY . .

RUN bun install
RUN bun run build

FROM oven/bun

COPY --from=builder /app/build /home/bun/app/build
COPY --from=builder /app/.env .
COPY --from=builder /app/server.js .
