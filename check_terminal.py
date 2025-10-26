from sgrml import SGR

print("Let's test basic SGR sequences.")
print("")

print(SGR("<b>Bold.</b>"))
print(SGR("<i>Italic.</i>"))
print(SGR("<b>Bold. <i>Italic and Bold.</b> Italic.</i> Normal."))

print("")
print(SGR("<u>Solid Underline.</u>"))
print(SGR("<u type=double>Double Underline.</u>"))
print(SGR("<u type=wavy>Wavy Underline.</u>"))
print(SGR("<u type=dotted>Dotted Underline.</u>"))
print(SGR("<u type=dashed>Dashed Underline.</u>"))

print("")
print(
    SGR(
        "<u type=wavy><b>Wavy Underline and Bold. <i><u type=solid>Solid Underline, Bold and Italic. </i></u>"
        "Wavy Underline and Bold. </b>Wavy Underline.</u>"
    )
)
