from pygments.token import Token
from nubia import context, statusbar


class PoEToolStatusBar(statusbar.StatusBar):

    def get_tokens(self):
        try:
            context.get_context().ggpk
            ggpk = (Token.Warn, "GGPK Loaded")
        except AttributeError:
            ggpk = (Token.Info, "No GGPK loaded")

        return [
            ggpk
        ]