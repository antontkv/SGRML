from sgrml import SGR

print("Let's test basic SGR sequences.")
print("")

# Bold, Dim, Italic
print(SGR("<b>Bold.</b>"))
print(SGR("<dim>Dim</dim>"))
print(SGR("<i>Italic.</i>"))
print(SGR("<b>Bold. <i>Italic and Bold. <dim>Dim, Italic and Bold.</dim></b> Italic.</i> Normal."))

# Underline
print("")
print(SGR("<u>Solid Underline.</u>"))
print(SGR("<u type=double>Double Underline.</u>"))
print(SGR("<u type=wavy>Wavy Underline.</u>"))
print(SGR("<u type=dotted>Dotted Underline.</u>"))
print(SGR("<u type=dashed>Dashed Underline.</u>"))

# Blink, Inverse
print("")
print(SGR("<blink type=slow>Slow Blink</blink>"))
print(SGR("<blink type=rapid>Rapid Blink</blink>"))
print(SGR("<inverse>Inverse: Swap foreground and background colors</inverse>"))

# Mix
print("")
print(
    SGR(
        "<u type=wavy><b>Wavy Underline and Bold. <i><u type=solid>Solid Underline, Bold and Italic. </i></u>"
        "Wavy Underline and Bold. </b>Wavy Underline.</u>"
    )
)
