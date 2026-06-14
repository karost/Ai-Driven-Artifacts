FROM ubuntu:24.04

ARG ROOT_PASSWORD
ARG THANIT_PASSWORD

RUN apt-get update && apt-get install -y openssh-server vim sudo git curl

RUN mkdir /var/run/sshd

# Set passwords
RUN echo "root:${ROOT_PASSWORD}" | chpasswd
RUN useradd -m -s /bin/bash thanit && echo "thanit:${THANIT_PASSWORD}" | chpasswd && usermod -aG sudo thanit

# SSH settings
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]