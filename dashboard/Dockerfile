FROM oven/bun AS builder

WORKDIR /app

COPY . .

RUN bun install
RUN bun run build

FROM oven/bun

COPY --from=builder /app/build .
COPY --from=builder /app/.env .
