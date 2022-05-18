#!/usr/bin/haserl
<%in _common.cgi %>
<%in _header.cgi %>
<%
page_title="$tPageTitleFormatCard"
card_partition="/dev/mmcblk0p1"

error=""
output=""
if [ ! -b $card_partition ]; then
  error="$tMsgNoCardPartition"
else
  if [ "$(grep $card_partition /dev/mtab)" ]; then
    command="umount $card_partition"
    output="${output}\n$(umount $card_partition 2>&1)"
    [ $? -ne 0 ] && error="$tMsgCannotUnmountCardPartition"
  else
    command="mkfs.vfat -v -n OpenIPC $card_partition"
    output="${output}\n$(mkfs.vfat -v -n OpenIPC $card_partition 2>&1)"
    if [ $? -ne 0 ]; then
      error="$tMsgCannotFormatCardPartition"
    else
      command="mount $card_partition"
      output="${output}\n$(mount $card_partition 2>&1)"
      [ $? -ne 0 ] && error="$tMsgCannotRemountCardPartition"
    fi
  fi
fi

if [ ! -z "$error" ]; then
  report_error "$error"
  [ ! -z "$command" ] && report_command_info "$command" "$output"
else
%>
<pre class="bg-light p-4 log-scroll">
<%= $output %>
</pre>
<% fi %>
<a class="btn btn-primary" href="/"><%= $tButtonGoHome %></a>
<%in _footer.cgi %>