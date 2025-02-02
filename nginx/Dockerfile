FROM nginx:1.25.5

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/nginx.conf

RUN mkdir -p /var/log/nginx && \
    chmod -R 755 /var/log/nginx && \
    chown -R nginx:nginx /var/log/nginx 