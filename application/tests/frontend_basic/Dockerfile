FROM angelalonso/arm32v6_reactjs:v0.02 AS builder
WORKDIR /app
RUN npm run build

FROM angelalonso/arm32v6_reactjs:v0.02
WORKDIR /app
COPY --from=builder /app/build .
RUN npm install -g serve
CMD ["serve", "-p", "80", "-s", "."]
