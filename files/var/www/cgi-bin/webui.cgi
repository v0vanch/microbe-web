#!/usr/bin/haserl
<%in p/common.cgi %>
<%
if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$POST_action" in
  init)
    update_caminfo
    redirect_back
    ;;
  *)
    redirect_to $SCRIPT_NAME "danger" "НЕИЗВЕСТНОЕ ДЕЙСТВИЕ: $POST_action"
    ;;
  esac
fi

page_title="Веб-интерфейс"

web_version="master"
[ -n "$ui_version" ] && web_version="$(echo "$ui_version" | cut -d+ -f1)"
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Версия</h3>
    <dl class="list small">
      <dt>Установленая</dt><dd><%= $ui_version %></dd>
      <dt>Последняя</dt><dd id="microbe-web-stk-ver"></dd>
      <%#
        <dt>Стабильная</dt><dd id="microbe-web-master-ver"></dd>
        <dt>Нестабильная</dt><dd id="microbe-web-dev-ver"></dd>
      %>
    </dl>
  </div>
  <div class="col">
    <h3>Обновление</h3>
  <% if [ -n "$network_gateway" ]; then %>
    <form action="webui-update.cgi" method="post">
      <% field_hidden "action" "update" %>
      <% field_hidden "web_version" "stk" %>
      <%# field_select "web_version" "Ветка" "master:Stable,dev:Development,stk:STK" %>
      <% field_checkbox "web_verbose" "Подробный вывод." %>
      <% field_checkbox "web_enforce" "Установить, даже если версия не поменялась." %>
      <% field_checkbox "web_noreboot" "Не перезагружать систему после обновления." %>
      <% button_submit "Установить обновление" "warning" %>
    </form>
  <% else %>
    <p class="alert alert-danger">Для обновления требуется доступ к GitHub.</p>
  <% fi %>
  </div>
</div>

<script>
const GH_URL="https://github.com/v0vanch/";
const GH_API="https://api.github.com/repos/v0vanch/";

function checkUpdates() {
  queryBranch('microbe-web', 'stk');
}

function queryBranch(repo, branch) {
  var oReq = new XMLHttpRequest();
  oReq.addEventListener("load", function(){
    const d = JSON.parse(this.response);
    const sha_short = d.commit.sha.slice(0,7);
    const date = d.commit.commit.author.date.slice(0,10);
    const text = document.createElement('span');
    text.textContent = branch + '+' + sha_short + ', ' + date;
    const el = $('#' + repo + '-' + branch + '-ver').appendChild(text);
  });
  oReq.open("GET", GH_API + repo + '/branches/' + branch);
  oReq.setRequestHeader("Authorization", "Basic " + btoa("<%= "${GITHUB_USERNAME}:${GITHUB_TOKEN}" %>"));
  oReq.send();
}

window.addEventListener('load', checkUpdates);
</script>
<%in p/footer.cgi %>
