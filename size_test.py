with open('size_test.html','w') as f:
    for i in range(30):
        f.write(f"<pre style='font-size: {i}pt;'>{i}pt, the quick brown fox jumps over the lazy dog</pre>")