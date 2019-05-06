FROM angelalonso/arm32v6_reactjs:0.01 AS builder
WORKDIR /app
COPY . .
RUN yarn run build

FROM angelalonso/arm32v6_reactjs:0.01
RUN yarn global add serve
WORKDIR /app
COPY --from=builder /app/build .
CMD ["serve", "-p", "80", "-s", "."]
