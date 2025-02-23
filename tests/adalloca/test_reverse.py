import sys 
sys.path.append("packages/adalloca/reverse")
import reverse

def test_reverse():
    res = reverse.reverse({})
    assert res["output"] == "reverse"
