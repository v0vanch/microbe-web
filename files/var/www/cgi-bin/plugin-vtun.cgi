#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="vtun"
plugin_name="Виртуальный Туннель"
page_title="Виртуальный Туннель"
service_file=/etc/init.d/S98vtun
conf_file=/tmp/vtund.conf

if [ -n "$POST_action" ] && [ "$POST_action" = "reset" ]; then
  killall tunnel
  killall vtund
  rm $conf_file
  rm $service_file
  redirect_to "$SCRIPT_NAME" "danger" "Туннель отключен"
fi

if [ -n "$POST_vtun_host" ]; then
  echo -e "#!/bin/sh\n\ntunnel $POST_vtun_host\n" >$service_file
  chmod +x $service_file
  $service_file
  redirect_to "$SCRIPT_NAME" "success" "Туннель включен"
fi
%>
<%in p/header.cgi %>

<div class="row g-4 mb-4">
  <div class="col col-lg-4">
  <% if [ -f "$conf_file" ]; then %>
    <div class="alert alert-success">
      <h4>Виртуальный туннель включен</h4>
      <p>ИСпользуйте следующие учетные данные, чтобы настроить удаленный доступ через активный виртуальный туннель:</p>
      <dl class="mb-0">
        <dt>ID туннеля</dt>
        <dd><%= ${network_macaddr//:/} | tr a-z A-Z %></dd>
        <dt>Пароль</dt>
        <dd><% grep password $conf_file | xargs | cut -d' ' -f2 | sed 's/;$//' %>
      </dl>
    </div>
  <% fi %>

    <h3>Settings</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
    <% if [ -f "$service_file" ]; then %>
      <% field_hidden "action" "reset" %>
      <% button_submit "Сбросить конфигурацию" %>
    <% else %>
      <% field_text "vtun_host" "Хост виртуального туннеля" "Адрес сервера виртуального туннеля." %>
      <% button_submit %>
    <% fi %>
    </form>
  </div>
  <div class="col col-lg-8">
    <h3>Файлы конфигурации</h3>
<%
[ -f "$service_file" ] && ex "cat $service_file"
[ -f "$conf_file" ] && ex "cat $conf_file"
ex "ps | grep tunnel"
ex "ps | grep vtund"
%>
  </div>
</div>

<%in p/footer.cgi %>
