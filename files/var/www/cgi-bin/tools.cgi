#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Инструменты мониторинга"
tools_action="${POST_tools_action:=ping}"
tools_target="${POST_tools_target:=4.2.2.1}"
tools_interface="${POST_tools_interface:=auto}"
tools_packet_size="${POST_tools_packet_size:=56}" # 56-1500 for ping, 38-32768 for trace
tools_duration="${POST_tools_duration:=5}"

if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$tools_action" in
    ping)
      title="Проверка ping"
      cmd="ping"
      [ "auto" != "$tools_interface" ] && cmd="$cmd -I $tools_interface"
      cmd="$cmd -s $tools_packet_size"
      cmd="$cmd -c $tools_duration"
      cmd="$cmd $tools_target"
      ;;
    trace)
      title="Проверка traceroute"
      cmd="traceroute"
      # order is important!
      cmd="$cmd -q $tools_duration"
      cmd="$cmd -w 1"
      [ "auto" != "$tools_interface" ] && cmd="$cmd -i $tools_interface"
      cmd="$cmd $tools_target"
      cmd="$cmd $tools_packet_size"
      ;;
    *)
      ;;
  esac
fi
%>
<%in p/header.cgi %>

<div class="row g-4 mb-4">
  <div class="col col-md-4">
    <h3>Проверка сети</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_select "tools_action" "Action" "ping,trace" %>
      <% field_text "tools_target" "Целевой FQDN или IP адрес" %>
      <% field_select "tools_interface" "Сетевой интерфейс" "auto,${interfaces}" %>
      <% field_number "tools_packet_size" "Размер пакета" "56,65535,1" "Bytes" %>
      <% field_number "tools_duration" "Кол-во пакетов" "1,30,1" %>
      <% button_submit "Запуск" %>
    </form>
  </div>
  <div class="col col-md-8">
    <h3><%= $title %></h3>
  <% if [ -n "$cmd" ]; then %>
    <h5># <%= $cmd %></h5>
    <pre id="output" data-cmd="<%= $cmd %>"></pre>
  <% fi %>
  </div>
</div>

<%in p/footer.cgi %>
