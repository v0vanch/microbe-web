#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="admin"
page_title="Admin profile"
params="name email telegram"

tmp_file=/tmp/${plugin}.conf
config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  [ -z "$admin_name"  ] && flash_append "danger" "Имя админа не может быть пустым." && error=1
  [ -z "$admin_email" ] && flash_append "danger" "Email админа не может быть пустым." && error=1
  # [ -z "$admin_telegram" ] && error="Telegram никнейм админа не может быть пустым."

  # add @ to Telegram username, if missed
  [ -n "$admin_telegram" ] && [ "${admin_telegram:0:1}" != "@" ] && admin_telegram="@$admin_telegram"

  if [ -z "$error" ]; then
    # create temp config file
    :>$tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >>$tmp_file
    done; unset _p
    mv $tmp_file $config_file

    update_caminfo
    redirect_back "success" "Профиль админа обновлен."
  fi
else
  include $config_file
fi
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Настройки</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "update" %>
      <% field_text "admin_name" "Полное имя админа" "будет использовано при отправке писем" %>
      <% field_text "admin_email" "Email адрес админа" %>
      <% field_text "admin_telegram" "Никнейм админа в Telegram" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <h3>Config file</h3>
    <% ex "cat $config_file" %>
  </div>
</div>

<%in p/footer.cgi %>
