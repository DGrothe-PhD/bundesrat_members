# Members of the German Bundesrat

# Usage
Go to: https://www.bundesrat.de/DE/bundesrat/mitglieder/mitglieder-node.html?cms_param3=Alle&cms_param2=contact&cms_param1=state-1
Save page with your browser to de-obfuscate javascript.

```
./parse.py
```

edit `bundesrat.json`, change `gender = '?'` to either `m` or `f`.

prettify
```
jq bundesrat.json > bundesrat_member.json
```

# License

Public Domain
