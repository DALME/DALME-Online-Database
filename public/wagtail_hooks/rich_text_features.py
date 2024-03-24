"""Enable extra rich text features."""


def enable_rich_text_features(features):
    features.default_features.append('superscript')
    features.default_features.append('subscript')
    features.default_features.append('strikethrough')
    features.default_features.append('code')
    features.default_features.append('blockquote')
