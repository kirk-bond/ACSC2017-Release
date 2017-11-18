####
#
# forgot_to_patch CTF challenge Dockerfile
#
# Build - Troy Ward - 1 NOV 17
####

FROM php:7.0-apache
RUN docker-php-ext-install mysqli
RUN apt-get update \
    && apt-get install -y zlib1g-dev \
    && rm -rf /var/lib/apt/lists/* \
    && docker-php-ext-install zip 
	
COPY ./20171016_justafakewordpresssite_162bbf985194aa348034171016012613_archive.zip /var/www/html/
COPY ./installer.php /var/www/html/

# Expose apache.
EXPOSE 80


