#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="motion"
plugin_name="Отслеживание движения"
page_title="Отслеживание движения"
params="enabled sensitivity send2email send2ftp send2telegram send2webhook send2yadisk playonspeaker throttle"

[ -n "$(echo "$mj_hide_motionDetect" | sed -n "/\b${soc_family}\b/p")" ] && redirect_to "/" "danger" "Определение движения не поддерживается на этой камере."

service_file=/etc/init.d/S92motion
tmp_file=/tmp/${plugin}

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Validation
  if [ "true" = "$motion_enabled" ]; then
    [ "false" = "$motion_send2email" ] && \
    [ "false" = "$motion_send2ftp" ] && \
    [ "false" = "$motion_send2telegram" ] && \
    [ "false" = "$motion_send2webhook" ] && \
    [ "false" = "$motion_send2yadisk" ] && \
    [ "false" = "$motion_playonspeaker" ] && \
    flash_append "danger" "Необходимо выбрать по крайней мере один вариант оповещения" && error=1
  fi

  if [ -z "$error" ]; then
    # create temp config file
    :>$tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >>$tmp_file
    done; unset _p
    mv $tmp_file $config_file

    if [ "true" = "$motion_enabled" ]; then
      if [ -z "$(eval echo "DEBUG TRACE" | sed -n "/\b$(yaml-cli -g .system.logLevel)\b/p")" ]; then
        # make required changes to majestic.yaml
        _t=$(mktemp)
        cp -f /tmp/majestic.yaml $_t
        yaml-cli -i $_t -s .system.logLevel DEBUG
        yaml-cli -i $_t -s .motionDetect.visualize true
        yaml-cli -i $_t -s .motionDetect.debug true
        mv -f $_t /tmp/majestic.yaml
        unset _t
      fi
      # touch /tmp/motionguard-restart.txt
      /etc/init.d/S92motion restart >/dev/null
    else
      /etc/init.d/S92motion stop >/dev/null
    fi

    update_caminfo
    redirect_to "$SCRIPT_NAME"
  fi
else
  include $config_file

  # Default values
  [ -z "$motion_sensitivity" ] && motion_sensitivity=45
  [ -z "$motion_throttle"    ] && motion_throttle=10
fi
%>
<%in p/header.cgi %>

<div class="row g-4 mb-4">
  <div class="col col-lg-4">
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "motion_enabled" "Включить определение движения" %>
      <% field_range "motion_sensitivity" "Чувствительность" "1,50,1" "1 - минимальная чувствительность, 50 - максимальная чувствительность" %>
      <% field_range "motion_throttle" "Задержка между уведомлениями, сек." "1,30,1" %>
      <% field_checkbox "motion_send2email" "Отправить по email" "<a href=\"plugin-send2email.cgi\">Настроить отправку по email</a>" %>
      <% field_checkbox "motion_send2ftp" "Отправить по FTP" "<a href=\"plugin-send2ftp.cgi\">Настроить отправку по FTP</a>" %>
      <% field_checkbox "motion_send2telegram" "Отправить через Telegram" "<a href=\"plugin-send2telegram.cgi\">Настроить отправку через Telegram</a>" %>
      <% field_checkbox "motion_send2webhook" "Отправить на веб-хук" "<a href=\"plugin-send2webhook.cgi\">Настроить отправку на веб-хук</a>" %>
      <% field_checkbox "motion_send2yadisk" "Отправить на Яндекс Диск" "<a href=\"plugin-send2yadisk.cgi\">Настроить отправку на Яндекс Диск</a>" %>
      <% field_checkbox "motion_playonspeaker" "Проиграть звуковой файл на динамике" "<a href=\"plugin-playonspeaker.cgi\">Настроить проигрывание звукового файла на динамике</a>" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col col-lg-8">
    <% [ -f $config_file ] && ex "cat $config_file" %>
    <% [ -f $service_file ] && ex "cat $service_file" %>
  </div>
</div>

<script>
<% [ "true" != "$email_enabled"    ] && echo "\$('#motion_send2email').disabled = true;" %>
<% [ "true" != "$ftp_enabled"      ] && echo "\$('#motion_send2ftp').disabled = true;" %>
<% [ "true" != "$telegram_enabled" ] && echo "\$('#motion_send2telegram').disabled = true;" %>
<% [ "true" != "$webhook_enabled"  ] && echo "\$('#motion_send2webhook').disabled = true;" %>
<% [ "true" != "$yadisk_enabled"   ] && echo "\$('#motion_send2yadisk').disabled = true;" %>
<% [ "true" != "$speaker_enabled"  ] && echo "\$('#motion_playonspeaker').disabled = true;" %>
</script>

<%in p/footer.cgi %>
