FROM jekyll/builder:latest

LABEL version="0.9.1"
LABEL description="develop and generate arc42.org site"
LABEL vendor="req42 (Peter Hruschka, Gernot Starke)"

COPY Gemfile .

RUN apk update && \
    apk add ncurses && \
    gem install bundler && \
    bundle install

WORKDIR /srv/jekyll
EXPOSE 4000
