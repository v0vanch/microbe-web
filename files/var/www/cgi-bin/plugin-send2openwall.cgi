#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="openwall"
plugin_name="Отправка на OpenWall"
page_title="Отправка на OpenWall"
params="enabled interval use_heif socks5_enabled"

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
  if [ "true" = "$openwall_enabled" ]; then
    [ "$openwall_interval" -lt "15" ] && flash_append "danger" "Установите интервал 15 минут или больше." && error=11
  fi

  if [ -z "$error" ]; then
    # create temp config file
    :>$tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >>$tmp_file
    done; unset _p
    mv $tmp_file $config_file

    # Disable/enable cron job
    cp /etc/crontabs/root /tmp/crontabs.tmp
    sed -i /send2openwall\.sh/d /tmp/crontabs.tmp
    [ "true" = "$openwall_enabled" ] &&
      echo "*/${openwall_interval} * * * * /usr/sbin/send2openwall.sh" >>/tmp/crontabs.tmp
    mv /tmp/crontabs.tmp /etc/crontabs/root

    update_caminfo
    redirect_back "success" "${plugin_name} конфигурация обновлена."
  fi

  redirect_to $SCRIPT_NAME
else
  include $config_file

  # Default values
  [ -z "$openwall_interval" ] && openwall_interval="15"
fi
%>
<%in p/header.cgi %>

<div class="alert alert-info">
<p>Этот плагин позволяет вам делиться изображениями с OpenIPC камеры на странице сайта <a href="https://openipc.org/open-wall">Open Wall</a>.
 Но это не все. Это сборщик полезных метрик. Изображения, которыми вы делитесь, позволяют нам определять
 качество изображений на различных камерах. Чтобы это делать, мы собираем следующую информацию: MAC адрес, модель SoC, модель сенсора, размер чипа памяти,
 версию прошивки и ап-тайм камеры.</p>
</div>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "openwall_enabled" "Включить отправку на OpenWall" %>
      <% field_select "openwall_interval" "Интервал, минуты" "15,30,60" "Время между отправлениями. 15 минут или больше." %>
      <% field_switch "openwall_use_heif" "Использовать HEIF формат." "Требуется H.265 кодек на Video0" %>
      <% field_switch "openwall_socks5_enabled" "Использовать SOCKS5" "<a href=\"network-socks5.cgi\">Настроить</a> SOCKS5 доступ" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <% ex "cat $config_file" %>
    <% ex "grep send2openwall /etc/crontabs/root" %>
    <% [ -f "/tmp/webui.log" ] && link_to "Скачать лог-файл" "dl.cgi" %>
  </div>
</div>

<% if [ "h265" != "$(yaml-cli -g .video0.codec)" ]; then %>
<script>
$('#openwall_use_heif').checked = false;
$('#openwall_use_heif').disabled = true;
</script>
<% fi %>

<%in p/footer.cgi %>
