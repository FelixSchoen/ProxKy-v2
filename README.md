# ProxKy

**ProxKy** is a fully automated custom proxy generator for the trading-card game *Magic: The Gathering*. It pulls data
from [Scryfall](https://scryfall.com/) and fills an InDesign template with the retrieved information.
**ProxKy** supports specification of the amount, set, collector's number and special printing flags for each card.

## Examples

We provide example images of four automatically generated cards, these
being [Black Lotus](https://scryfall.com/card/ovnt/2017NA/black-lotus)
, [Underground Sea](https://scryfall.com/card/vma/323/underground-sea)
, [Jace, the Mind Sculptor](https://scryfall.com/card/2xm/56/jace-the-mind-sculptor)
, [Brisela, Voice of Nightmares](https://scryfall.com/card/emn/15b/brisela-voice-of-nightmares)
, [Mountain](https://scryfall.com/card/vow/401/mountain)
, [Murderous Rider](https://scryfall.com/card/eld/97/murderous-rider-swift-end)
, [Paladin Class](https://scryfall.com/card/afr/29/paladin-class),
and [The Eldest Reborn](https://scryfall.com/card/c19/131/the-eldest-reborn). Note that these were generated using
version 1.0 of **ProxKy**.

<img src="data/examples/2017NA%20-%20Black%20Lotus.png" alt="drawing" width="200"/><img src="data/examples/323%20-%20Underground%20Sea.png" alt="drawing" width="200"/><img src="data/examples/56%20-%20Jace,%20the%20Mind%20Sculptor.png" alt="drawing" width="200"/><img src="data/examples/15b%20-%20Brisela,%20Voice%20of%20Nightmares.png" alt="drawing" width="200"/>

<img src="data/examples/401%20-%20Mountain.png" alt="drawing" width="200"/><img src="data/examples/97%20-%20Murderous%20Rider.png" alt="drawing" width="200"/><img src="data/examples/29%20-%20Paladin%20Class.png" alt="drawing" width="200"/><img src="data/examples/131%20-%20The%20Eldest%20Reborn.png" alt="drawing" width="200"/>

Note that the literal and graphical content provided is copyright of Wizards of the Ceast, LLC. All images provded serve
as fan content, permitted under the WotC fan content policy.

## Changelog

### Version 1.0

- Initial release

## Guides

This section provides readers with some information on how to e.g. format their decks lists in order to make **ProxKy**
able to parse them.

### Decklist Formatting

Note that **ProxKy** is only able to parse decklists in the form of *.txt files, where each entry corresponds to exactly
one card. No line may be empty. At the moment, **ProxKy** does not support comments, although support for this feature
is planned. The general format of a line in a decklist is as follows:

> {Amount} {Cardname} *[{Flags}]*

Note that text in italics represents an *optional* argument, meaning that it is not required for all cards and can
rather be used to make some adjustments for specific ones. An example of the above syntax would be as follows (note that
for the third entry we used one of the optional arguments):

> 5 Black Lotus  
> 1 Far // Away  
> 3 Mox Diamond [set: V10]

For an explanation of which optional arguments are available, what they do and how to use them, we refer to the
section [Parameters](#parameters).

Generally, and entry will correspond to the card first found using a standard search
on [Scryfall](https://scryfall.com/). Although this means that e.g. artwork, set information like rarity, and other
information of this nature depends on the exact card found, the printed rules text corresponds to the internal *oracle
text*, which is the same across **all versions of a card**. Due to this fact, it is usually sufficient to only provide
the name of one face of a card (in case of multi-faced cards, such as `Clearwater Pathway`).

### Parameters

These special arguments allow for further customization. For example, the exact version of a card can be defined (in
case there are several version, and one prefers artwork of one version over the other), or some style choices can be
made. Multiple arguments can be used for a single card, in this case they need to be separated using <code>
,&nbsp;</code> (a comma and a whitespace).

We provide an example of the use of such arguments:

> 1 Black Lotus [set: OVNT]  
> 1 Lotus Cobra [set: ZNR, cnr: 307]  
> 1 Kozilek, Butcher of Truth [tba: front]  
> 1 Nicol Bolas, the Ravager [tba: both]  
> 1 Gisela, the Broken Blade [tba: back]

In the following, we will discuss the exact usage and effect of the parameters.

#### Parameter "set"

Using this parameter, we can define the exact set which a card is pulled from. This is useful in case there are several
printings, which differ in e.g. artwork. The exact syntax is `set: {SET}`, were `{SET}` is to be replaced with the (all
uppercase) 3 to 5 letters uniquely identifying a set. Example:

> 1 Black Lotus [set: OVNT]

In this case, the card `Black Lotus` is pulled from the "Vintage Championship" set, which is not its default set when
searching for it on scryfall.

#### Parameter "cnr"

Using this parameter, we can define the collector's number of a card **in addition to its set**. Note that this **only
works when also specifying a set**, since collector numbers are not unique across sets. Example:

> 1 Lotus Cobra [set: ZNR, cnr: 307]

In this case the `Lotus Cobra` card with collector's number 307 in the set Zendikar Rising will be retrieved, which is
not the standard when searching for it. This card has a special artwork, which will then be used by **ProxKy**.

#### Parameter "id"

Using this parameter we can uniquely describe a card in the database of [Scryfall](https://scryfall.com/), although this
process is rather tedious. It can be useful for cards which cannot be otherwise fetched using the search function, e.g.
tokens. The internal id value can be found by clicking on "Copy-pastable JSON" under "IMAGES AND DATA" on the Scryfall
page of a card, and then copying the value (without quotation marks) which is under the "id" entry. Example:

> 1 Treasure [id: a3a684b7-27e0-4d9e-a064-9e03c6e50c89]

This results in a `Treasure` token being printed, in this case from the set Adventures in the Forgotten Realms Tokens.
We once again remark upon the fact that this method should only be used for cards where specification over set and
collector's number is not possible.

#### Parameter "tba"

This parameter results in a style choice which can be made for cards. It stands for "transparent body artwork", and once
applied will make the lower half of the card (containing rules text and so on) slightly transparent. This provides a
visual distinction from other cards, and can make certain special cards feel more valuable. It is very important to note
that this approach **does only work for cards where high-reolution artwork is locally stored**, and **not** for cards
where the artwork is automatically retrieved from [Scryfall](https://scryfall.com/) (which is almost all of them).

It is usually best to assume that no such artwork already exists. In this case we recommend checking
out [Art of MTG](https://www.artofmtg.com/), which often provide such artwork. If it does not exist on that page,
conducting a quick Google search often yields usable results. We refer to
section [Providing High-Resolution Artwork](#providing-high-resolution-artwork) on information on how to provide this
artwork yourself.

This parameter takes as input either the value "front", "back" or "both", which directly correspond to which face of a
card to apply the style choice to. The latter two parameters only work for cards which actually have a backside. An
example:

> 1 Gisela, the Broken Blade [tba: back]

In this case, the front side of the card, representing `Gisela, the Broken Blade`, will remain normal. Only the backside
of the card, containing `Brisela, Voice of Nightmares` will have the special transparency effect.

### Providing High-Resolution Artwork

In case you insist on using the "tba" parameter, you **have** to make sure that high-resolution artwork of the cards
exists. Since this artwork can only be manually downloaded and cannot be automated, the only option is to manually add
it to the database. In order to do so, decide on which version of the card you want to use (using
the [Scryfall](https://scryfall.com/)) platform. note the name, set and collector's number of the card. Proceed to find
high-resolution artwork of this card afterwards.

After finding such artwork it is **very** important how this artwork is saved, otherwise it will not be found by the
program. In the root folder (containing all the different artwork, e.g. a folder called "Artwork") create a folder for
each set that you found artwork for. Then, save the artwork under the corresponding folder, **using the following
format**:

> [Collector's Number] - [Cardname]

For example, if you want to provide artwork for `Black Lotus` of the Vintage Masters set, and a few other cards, your
folder structure would have to look like this:

```
Artwork
    \ EMN
        \ 15a - Bruna, the Fading Light.png
        \ 15b - Brisela, Voice of Nightmares.png
        \ 28 - Gisela, the Broken Blade.jpg
    \ UMA
        \ 6 - Kozilek, Butcher of Truth.jpg
        \ 250 - Rogue's Passage.jpg
    \ VMA
        \ 4 - Black Lotus.png
    \ ZNR
        \ 189 - Kazandu Mammoth.png
        \ 189 - Kazandu Valley.jpg
```

Note that the collector's number has to correspond to the number in Scryfall, **not** to the one printed on the card.

The above example also shows how to provide images for double faced cards (using `Bruna, the Fading Light`
and `Kazandu Mammoth`). If the backside contains an entirely different card (as is the case for meld cards), the
collector's number for the two faces will differ, otherwise simply provide two files with the same collector's number
but different card names. The program will use them for the front- and back faces respectively.

Finally, after having created this structure, zip the files and send them to me via any means possible. I will them add
them to the database, and they will automatically be used for the program. This can be done for any cards where you
would prefer higher-resolution artwork instead of the (low resolution) Scryfall one.

## License

As of time of writing, we are not making the required templates publicly available.