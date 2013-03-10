# -*- coding: utf-8 -*-
from collections import defaultdict

class Node(object):
    def __init__(self, weight, left=None, right=None):
        self.weight = weight
        self.left = left
        self.right = right
        self.score = None

    def __str__(self):
        return 'weight:%d,score:%s'%(self.weight,str(self.score))

    def address(self, score, from_parent=None):
        self.score=score
        if from_parent:
            self.score = from_parent+self.score
        if self.left:
            self.left.address('0', self.score)
        if self.right:
            self.right.address('1', self.score)

class Leaf(Node):
    def __init__(self, data, weight):
        self.data = data
        super(Leaf, self).__init__(weight)
    
    def __str__(self):
        return 'data:%s,'%str(self.data)+super(Leaf, self).__str__()

def gen_codes(tree):
    char_codes = {}
    if isinstance(tree, Leaf):
        char_codes[tree.data] = tree.score
    if tree.left:
        char_codes.update(gen_codes(tree.left))
    if tree.right:
        char_codes.update(gen_codes(tree.right))
    return char_codes
        
def encode(inp):
    freqs = defaultdict(int)
    freqs['EOT'] = 0
    for ch in inp: freqs[ch] += 1
    freqs = [Leaf(key,val) for key,val in freqs.items()]
    while len(freqs) > 1:
        freqs = sorted(freqs, key=lambda item: item.weight)
        low1 = freqs.pop(0)
        low2 = freqs.pop(0)
        node = Node(low1.weight+low2.weight, low1,low2)
        freqs.append(node)
    tree = freqs[0]
    tree.address('')
    codes = gen_codes(tree)
    bindata = str()
    for ch in inp: 
        bindata += codes[ch]
    bindata += codes['EOT']
    byte_len=8
    bindata += '0'*(len(bindata)%byte_len)
    index = 0
    encoded = []
    while index < len(bindata):
        encoded.append(int(bindata[index:index+byte_len],2))
        index += byte_len
    return codes, encoded

def check(pair, word):
    if pair[1] == word:
        return pair
    
def decode(code, encoded):
    tmp = str()
    out = str()
    for x in encoded:
        bit = 7
        while bit >= 0:
            tmp += str((x >> bit) & 0x1)
            bit -= 1
            match = filter(lambda x: check(x, tmp), code.items())
            if match:
                ch = match[0][0]
                if ch == 'EOT':
                    # Hit the End of text marker
                    break
                out += ch
                tmp = ''
    return out

if __name__ == '__main__':
    inp = '''
Earendil was a mariner
that tarried in Arvernien;
he built a boat of timber felled
in Nimbrethil to journey in;
her sails he wove of silver fair,
of silver were her lanterns made,
her prow was fashioned like a swan
and light upon her banners laid.

In panolpy of ancient kings,
in chained rings he armoured him;
his shining shield was scored with runes
to ward all wounds and harm from him;
his bow was made of dragon-horn,
his arrows shorn of ebony;
of silver was his habergeon,
his scabbard of chalcedony;
his sword of steel was valient,
of adamant his helmet tall,
an eagle-plume upon his crest,
upon his breast an emerald.

Beneath the Moon and under star
he wandered far from northern strands,
bewildered on enchanted ways
beyond the days of mortal lands.

From gnashing of the Narrow Ice
where shadow lies on frozen hills,
from nether heats and burning waste
he turned in haste, and roving still
on starless waters far astray
at last he came to Night of Naught,
and passed, and never sight he saw
of shining shore nor light he sought.

The winds of wrath came driving him,
and blindly in the foam he fled
from west to east and errandless,
unheralded he homeward sped.

There flying Elwing came to him,
and flame was in the darkness lit;
more bright than light of diamond
the fire on her carcanet.

The Silmaril she bound on him
and crowned him with the living light,
and dauntless then with burning brow
he turned his prow; and in the night
from otherworld beyond the Sea
there strong and free a storm arose,
a wind of power in Tarmenel;
by paths that seldom mortal goes
his boat it bore with biting breath
as might of death across the grey
and long forsaken seas distressed;
from east to west he passed away.

Thought Evernight he back was borne
on black and roaring waves that ran
o'er leagues unlit and foundered shores
that drowned before the Days began,
until he hears on strands of pearl
where end the world the music long,
where ever-foaming billows roll
the yellow gold and jewels wan.

He saw the Mountain silent rise
where twilight lies upon the knees
of Valinor, and Eldamar
beheld afar beyond the seas.

A wanderer escaped from night
to haven white he came at last,
to Elvenhome the green and fair
where keen the air, where pale as glass
beneath the Hill of Ilmarin
a-glimmer in a valley sheer
the lamplit towers of Tirion
are mirrored on the Shadowmere.

He tarried there from errantry,
and melodies they taught to him,
and sages old him marvels told,
and harps of gold they brought to him.

They clothed him then in elven-white,
and seven lights before him sent,
as through the Calacirian
to hidden land forlorn he went.

He came unto the timeless halls
where shining fall the countless years,
and endless reigns the Elder King
in Ilmarin on Mountain sheer;
and words unheard were spoken then
of folk and Men and Elven-kin,
beyond the world were visions showed
forbid to those that dwell therein.

A ship then new they built for him
of mithril and of elven glass
with shining prow; no shaven oar
nor sail she bore on silver mast:
the Silmaril as lantern light
and banner bright with living flame
to gleam thereon by Elbereth
herself was set, who thither came
and wings immortal made for him,
and laid on him undying doom,
to sail the shoreless skies and come
behind the Sun and light of Moon.

From Evergreen's lofty hills
where softly silver fountains fall
his wings him bore, a wandering light,
beyond the mighty Mountain Wall.

From a World's End there he turned away,
and yearned again to find afar
his home through shadows journeying,
and burning as an island star
on high above the mists he came,
a distant flame before the Sun,
a wonder ere the waking dawn
where grey the Norland waters run.

And over Middle-Earth he passed
and heard at last the weeping sore
of women and of elven-maids
in Elder Days, in years of yore.

But on him mighty doom was laid,
till Moon should fade, an orbed star
to pass, and tarry never more
on Hither Shores where Mortals are;
or ever still a herald on
an errand that should never rest
to bear his shining lamp afar,
to Flammifer of Westernesse.
'''
    code, encoded = encode(inp)
    decoded = decode(code, encoded)
    print 'Original text size in bytes: %d'%len(inp)
    print 'Encoded text size in bytes: %d'%len(encoded)
    print inp == decoded

