#!/usr/bin/haserl
<%in p/common.cgi %>
<%
filepath=$(mktemp)
filename="$GET_log"

case "$filename" in
  dmesg)
    dmesg >$filepath
    ;;
  logread)
    logread >$filepath
    ;;
  netstat)
    netstat -a >$filepath
    ;;
  *)
    echo "Неизвестный файл."
    exit 1
esac

[ ! -f "$filepath" ] && redirect_back "danger" "Файл ${filename} не найден"

echo "HTTP/1.0 200 OK
Date: $(time_http)
Server: $SERVER_SOFTWARE
Content-type: text/plain
Content-Disposition: attachment; filename=${filename}-$(date +%s).txt
Content-Length: $(wc -c $filepath | cut -d' ' -f1)
Cache-Control: no-store
Pragma: no-cache
"
cat ${filepath}
rm ${filepath}
%>
