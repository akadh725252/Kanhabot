# kanha - UserBot
# Copyright (C) 2021-2023 Teamkanha
# This file is a part of < https://github.com/Teamkanha/kanha/ >
# PLease read the GNU Affero General Public License in <https://www.github.com/Teamkanha/kanha/blob/main/LICENSE/>.

FROM theteamkanha/kanha:main

# set timezone
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY installer.sh .

RUN bash installer.sh

# changing workdir
WORKDIR "/root/Teamkanha"

# start the bot.
CMD ["bash", "startup"]
