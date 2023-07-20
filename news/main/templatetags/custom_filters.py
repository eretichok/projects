from django import template

register = template.Library()

# Грубый фильтр цензуры (находит совпадение в словаре грубых слов bad_words и меняет их на *
@register.filter()
def apply_censor(text):
    bad_words = ['bad_word', ]
    res = ''
    for word in text.split():
        if word.strip('.,;:-?!()').lower() in bad_words:
            bad_word = word.strip('.,;:-?!()').lower()
            for l in word.lower():
                if l != bad_word[0]:
                    res += l
                else:
                    break
            temp = ''
            for l in word.lower()[-1]:
                if l != bad_word[-1]:
                    temp += l
                else:
                    break
            res += '*' + temp
        else:
            res += word + ' '
    return res
