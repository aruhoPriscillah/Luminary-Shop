from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review, Order

UGANDA_DISTRICTS = [
    ('', '-- Select District --'),
    ('Abim', 'Abim'),
    ('Adjumani', 'Adjumani'),
    ('Agago', 'Agago'),
    ('Alebtong', 'Alebtong'),
    ('Amolatar', 'Amolatar'),
    ('Amudat', 'Amudat'),
    ('Amuria', 'Amuria'),
    ('Amuru', 'Amuru'),
    ('Apac', 'Apac'),
    ('Arua', 'Arua'),
    ('Budaka', 'Budaka'),
    ('Bududa', 'Bududa'),
    ('Bugiri', 'Bugiri'),
    ('Bugweri', 'Bugweri'),
    ('Buhweju', 'Buhweju'),
    ('Buikwe', 'Buikwe'),
    ('Bukedea', 'Bukedea'),
    ('Bukomansimbi', 'Bukomansimbi'),
    ('Bukwo', 'Bukwo'),
    ('Bulambuli', 'Bulambuli'),
    ('Buliisa', 'Buliisa'),
    ('Bundibugyo', 'Bundibugyo'),
    ('Bunyangabu', 'Bunyangabu'),
    ('Bushenyi', 'Bushenyi'),
    ('Busia', 'Busia'),
    ('Butaleja', 'Butaleja'),
    ('Butebo', 'Butebo'),
    ('Buvuma', 'Buvuma'),
    ('Buyende', 'Buyende'),
    ('Dokolo', 'Dokolo'),
    ('Gomba', 'Gomba'),
    ('Gulu', 'Gulu'),
    ('Hoima', 'Hoima'),
    ('Ibanda', 'Ibanda'),
    ('Iganga', 'Iganga'),
    ('Isingiro', 'Isingiro'),
    ('Jinja', 'Jinja'),
    ('Kaabong', 'Kaabong'),
    ('Kabale', 'Kabale'),
    ('Kabarole', 'Kabarole'),
    ('Kaberamaido', 'Kaberamaido'),
    ('Kagadi', 'Kagadi'),
    ('Kakumiro', 'Kakumiro'),
    ('Kalaki', 'Kalaki'),
    ('Kalangala', 'Kalangala'),
    ('Kaliro', 'Kaliro'),
    ('Kalungu', 'Kalungu'),
    ('Kampala', 'Kampala'),
    ('Kamuli', 'Kamuli'),
    ('Kamwenge', 'Kamwenge'),
    ('Kanungu', 'Kanungu'),
    ('Kapchorwa', 'Kapchorwa'),
    ('Kapelebyong', 'Kapelebyong'),
    ('Karenga', 'Karenga'),
    ('Kasanda', 'Kasanda'),
    ('Kasese', 'Kasese'),
    ('Katakwi', 'Katakwi'),
    ('Kayunga', 'Kayunga'),
    ('Kazo', 'Kazo'),
    ('Kibaale', 'Kibaale'),
    ('Kiboga', 'Kiboga'),
    ('Kibuku', 'Kibuku'),
    ('Kikuube', 'Kikuube'),
    ('Kiruhura', 'Kiruhura'),
    ('Kiryandongo', 'Kiryandongo'),
    ('Kisoro', 'Kisoro'),
    ('Kitagwenda', 'Kitagwenda'),
    ('Kitgum', 'Kitgum'),
    ('Koboko', 'Koboko'),
    ('Kole', 'Kole'),
    ('Kotido', 'Kotido'),
    ('Kumi', 'Kumi'),
    ('Kwania', 'Kwania'),
    ('Kween', 'Kween'),
    ('Kyankwanzi', 'Kyankwanzi'),
    ('Kyegegwa', 'Kyegegwa'),
    ('Kyenjojo', 'Kyenjojo'),
    ('Kyotera', 'Kyotera'),
    ('Lamwo', 'Lamwo'),
    ('Lira', 'Lira'),
    ('Luuka', 'Luuka'),
    ('Luwero', 'Luwero'),
    ('Lwengo', 'Lwengo'),
    ('Lyantonde', 'Lyantonde'),
    ('Madi-Okollo', 'Madi-Okollo'),
    ('Manafwa', 'Manafwa'),
    ('Maracha', 'Maracha'),
    ('Masaka', 'Masaka'),
    ('Masindi', 'Masindi'),
    ('Mayuge', 'Mayuge'),
    ('Mbale', 'Mbale'),
    ('Mbarara', 'Mbarara'),
    ('Mitooma', 'Mitooma'),
    ('Mityana', 'Mityana'),
    ('Moroto', 'Moroto'),
    ('Moyo', 'Moyo'),
    ('Mpigi', 'Mpigi'),
    ('Mubende', 'Mubende'),
    ('Mukono', 'Mukono'),
    ('Nabilatuk', 'Nabilatuk'),
    ('Nakapiripirit', 'Nakapiripirit'),
    ('Nakaseke', 'Nakaseke'),
    ('Nakasongola', 'Nakasongola'),
    ('Namayingo', 'Namayingo'),
    ('Namisindwa', 'Namisindwa'),
    ('Namutumba', 'Namutumba'),
    ('Napak', 'Napak'),
    ('Nebbi', 'Nebbi'),
    ('Ngora', 'Ngora'),
    ('Ntoroko', 'Ntoroko'),
    ('Ntungamo', 'Ntungamo'),
    ('Nwoya', 'Nwoya'),
    ('Obongi', 'Obongi'),
    ('Omoro', 'Omoro'),
    ('Otuke', 'Otuke'),
    ('Oyam', 'Oyam'),
    ('Pader', 'Pader'),
    ('Pakwach', 'Pakwach'),
    ('Pallisa', 'Pallisa'),
    ('Rakai', 'Rakai'),
    ('Rubanda', 'Rubanda'),
    ('Rubirizi', 'Rubirizi'),
    ('Rukiga', 'Rukiga'),
    ('Rukungiri', 'Rukungiri'),
    ('Rwampara', 'Rwampara'),
    ('Sembabule', 'Sembabule'),
    ('Serere', 'Serere'),
    ('Sheema', 'Sheema'),
    ('Sironko', 'Sironko'),
    ('Soroti', 'Soroti'),
    ('Tororo', 'Tororo'),
    ('Wakiso', 'Wakiso'),
    ('Yumbe', 'Yumbe'),
    ('Zombo', 'Zombo'),
]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=150, label='Full Name')
    email = forms.EmailField(label='Email Address')
    address = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'rows': 2}))
    city = forms.CharField(max_length=100, label='Town/Village')
    district = forms.ChoiceField(choices=UGANDA_DISTRICTS, label='District')


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your experience…'}),
        }


class ProductSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Search', widget=forms.TextInput(
        attrs={'placeholder': 'Search products…'}
    ))