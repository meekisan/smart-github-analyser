FROM nimmis/apache-php7
EXPOSE 80
RUN apt-get update && apt-get install -y php7.0-bcmath php7.0-mbstring
ADD 000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./src/* /var/www/
WORKDIR /var/www/
RUN php composer.phar update
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
