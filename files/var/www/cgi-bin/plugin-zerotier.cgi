#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="zerotier"
plugin_name="ZeroTier"
page_title="ZeroTier"
params="enabled nwid"

[ ! -f /usr/sbin/zerotier-cli ] && redirect_to "/" "danger" "ZerotierOne клиент не является частью вашей прошивки."

tmp_file=/tmp/${plugin}.conf

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

service_file=/etc/init.d/S90zerotier
zt_cli_bin=/usr/sbin/zerotier-cli
zt_one_bin=/usr/sbin/zerotier-one

[ "ultimate" != "$fw_variant" ] &&
  redirect_to "/" "danger" "ZeroTier плагин не поддерживается на OpenIPC ${fw_variant}."
[ ! -f "$zt_one_bin" ] &&
  redirect_to "/" "danger" "${zt_one_bin} файл не найден."
[ ! -f "$service_file" ] &&
  redirect_to "/" "danger" "${service_file} файл не найден."

include $config_file
[ -n "$zerotier_nwid" ] && zt_network_config_file="/var/lib/zerotier-one/networks.d/${zerotier_nwid}.conf"

if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$POST_action" in
  create)
    # parse values from parameters
    for _p in $params; do
      eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
      sanitize "${plugin}_${_p}"
    done; unset _p

    ### Validation
    if [ "true" = "$zerotier_enabled" ]; then
      [ -z "$zerotier_nwid" ] &&
        flash_append "danger" "ZeroTier Network ID не можеть быть пустым." && error=1
      [ "${#zerotier_nwid}" -ne "16" ] &&
        flash_append "danger" "ZeroTier Network ID должен состоять из 16 цифр." && error=2
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
    ;;
  start|open)
    $service_file start >&2
    redirect_back # "success" "Сервис запущен"
    ;;
  stop|close)
    $service_file stop >&2
    redirect_back # "danger" "Сервис остановлен"
    ;;
  join)
    $zt_cli_bin join $zerotier_nwid >&2
    while [ -z $(grep nwid "$zt_network_config_file") ]; do sleep 1; done
    redirect_back
    ;;
  leave)
    $zt_cli_bin leave $zerotier_nwid >&2
    redirect_back
    ;;
  *)
    redirect_back "danger" "Неизвестное действие $POST_action!"
  esac
fi
%>
<%in p/header.cgi %>

<div class="row g-4 mb-4">
  <div class="col col-lg-4">
    <h3>Настройки</h3>

    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "create" %>
      <% field_switch "zerotier_enabled" "Включить ZeroTier сеть при перезагрузке" %>
      <% field_text "zerotier_nwid" "ZeroTier ID Сети" "Нет ID сети? Получите на <a href=\"https://my.zerotier.com/\">my.zerotier.com</a>" %>
      <% button_submit %>
    </form>

    <br>

    <% zerotier-cli info >/dev/null; if [ $? -eq 0 ]; then %>
      <div class="alert alert-success">
        <h5>ZeroTier туннель открыт</h5>

        <% if [ -f "$zt_network_config_file" ]; then %>
          <% zt_id="$(grep ^nwid= ${zt_network_config_file} | cut -d= -f2)" %>
          <% zt_name="$(grep ^n= ${zt_network_config_file} | cut -d= -f2)" %>
          <% if [ -n "$zt_id" ] && [ -n "$zt_name" ]; then %>
            <p>ИСпользуйте следующие учетные данные, чтобы настроить удаленный доступ через активный виртуальный туннель:</p>
            <dl>
              <dt>NWID: <%= $zt_id %></dd>
              <dt>Name: <%= $zt_name %></dd>
            </dl>
            <form action="<%= $SCRIPT_NAME %>" method="post">
              <% field_hidden "action" "leave" %>
              <% button_submit "Покинуть сеть" "danger" %>
            </form>
          <% fi %>
        <% else %>
          <div class="row">
            <div class="col">
              <form action="<%= $SCRIPT_NAME %>" method="post">
                <% field_hidden "action" "join" %>
                <% button_submit "Присоединиться к сети" %>
              </form>
            </div>
            <div class="col">
              <form action="<%= $SCRIPT_NAME %>" method="post">
                <% field_hidden "action" "stop" %>
                <% button_submit "Закрыть туннель" "danger" %>
              </form>
            </div>
          </div>
        <% fi %>
      </div>
    <% else %>
      <div class="alert alert-warning">
        <h4>ZeroTier туннель закрыт</h4>
        <form action="<%= $SCRIPT_NAME %>" method="post">
          <% field_hidden "action" "start" %>
          <% button_submit "Открыть туннель" %>
        </form>
      </div>
    <% fi %>
  </div>

  <div class="col col-lg-8">
    <h3>Файлы конфигурации</h3>
<%
[ -f "$service_file" ] && ex "cat $service_file"
[ -f "$config_file" ] && ex "cat $config_file"
[ -f "$zt_network_config_file" ] && ex "cat $zt_network_config_file"
ex "ps | grep zerotier"
%>
  </div>
</div>

<%in p/footer.cgi %>
