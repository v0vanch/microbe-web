#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="telegram"
plugin_name="Отправка через Telegram"
page_title="Отправка через Telegram"
params="enabled token as_attachment as_photo channel socks5_enabled"

tmp_file=/tmp/${plugin}.conf

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Validation
  if [ "true" = "$telegram_enabled" ]; then
    [ -z "$telegram_token"   ] && flash_append "danger" "Telegram токен не может быть пустым." && error=11
    [ -z "$telegram_channel" ] && flash_append "danger" "Telegram канал не может быть пустым." && error=12
  fi

  if [ -z "$error" ]; then
    # create temp config file
    :>$tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >>$tmp_file
    done; unset _p
    mv $tmp_file $config_file

    update_caminfo
    redirect_back "success" "${plugin_name} конфигурация обновлена."
  fi

  redirect_to $SCRIPT_NAME
else
  include $config_file
fi
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "telegram_enabled" "Включить отправку через Telegram" %>
      <% field_text "telegram_token" "Токен" "Аутентификационный токен вашего Telegram бота." %>
      <% field_text "telegram_channel" "ID чата" "Числовой ID канала, в который боту будет отправлять изображения." %>
      <% field_switch "telegram_as_photo" "Отправлять как фото." %>
      <% field_switch "telegram_as_attachment" "Отправлять как вложение." %>
      <% field_switch "telegram_socks5_enabled" "Использовать SOCKS5" "<a href=\"network-socks5.cgi\">Настроить</a> SOCKS5 доступ" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <% ex "cat $config_file" %>
    <% [ -f "/tmp/webui.log" ] && link_to "Скачать лог-файл" "dl.cgi" %>
  </div>
</div>

<% if [ -z "$telegram_token" ]; then %>
<div class="alert alert-info mt-4">
  <h5>Чтобы создать Telegram бота:</h5>
  <ol>
    <li>Начните чат с <a href=\"https://t.me/BotFather\">@BotFather</a></li>
    <li>Введите <code>/start</code>, чтобы начать сессию.</li>
    <li>Введите <code>/newbot</code>, чтобы создать нового бота.</li>
    <li>Задайте логин для бота, например, <i>cool_cam_bot</i>.</li>
    <li>Задайте никнейм для бота, например, <i>CoolCamBot</i>.</li>
    <li>Скопируйте токен выданный BotFather, и вставьте его в эту форму.</li>
  </ol>
</div>
<% fi %>

<%in p/footer.cgi %>
