#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="SD Card" %>
<%in p/header.cgi %>
<%
ls /dev/mmc* >/dev/null 2>&1
if [ $? -ne 0 ]; then
%>
<div class="alert alert-danger">
  <h4>Эта камера поддерживает SD карты?</h4>
  <p>У камеры нет слота для SD карт или SD карта не вставлена.</p>
</div>
<%
else
  card_device="/dev/mmcblk0"
  card_partition="${card_device}p1"
  mount_point="${card_partition//dev/mnt}"
  error=""
  _o=""
  if [ -n "$POST_doFormatCard" ]; then
%>
<div class="alert alert-danger">
  <h4>ВНИМАНИЕ! Форматирование SD карты займет время.</h4>
  <p>Пожалуйста, не обновляйте эту страницу. Подождите пока форматирование разделов закончится!</p>
</div>
<%
    if [ "$(grep $card_partition /etc/mtab)" ]; then
      _c="umount $card_partition"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="Не удалось размонтировать раздел SD карты."
    fi

    if [ -z "$error" ]; then
      _c="echo -e 'o\nn\np\n1\n\n\nw'|fdisk $card_device"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="Не удалось создать раздел SD карты."
    fi

    if [ -z "$error" ]; then
      _c="mkfs.vfat -v -n OpenIPC $card_partition"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="Не удалось отформатировать раздел SD карты."
    fi

    if [ -z "$error" ] && [ ! -d "$mount_point" ]; then
      _c="mkdir -p $mount_point"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="Не удалось создать точку монтирования SD карты."
    fi

    if [ -z "$error" ]; then
      _c="mount $card_partition $mount_point"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="Не удалось перемонтировать раздел SD карты."
    fi

    if [ -n "$error" ]; then
      report_error "$error"
      [ -n "$_c" ] && report_command_info "$_c" "$_o"
    else
      report_log "$_o"
    fi
%>
<a class="btn btn-primary" href="/">На главную</a>
<% else %>
<h4># df -h | sed -n "1p/<%= ${card_partition////\\\/} %>/p"</h4>
<pre class="small"><% df -h | sed -n "1p/${card_partition////\\\/}/p" %></pre>

<div class="alert alert-danger">
  <h4>ВНИМАНИЕ! Форматирование уничтожит все данные на SD карте.</h4>
  <p>Убедитесь, что у вас есть бэкап, если вы собираетесь использовать эти данные в будущем.</p>
  <form action="<%= $SCRIPT_NAME %>" method="post">
    <% field_hidden "doFormatCard" "true" %>
    <% button_submit "Форматировать SD карту" "danger" %>
  </form>
</div>
<%
  fi
fi
%>
<%in p/footer.cgi %>
