from django import forms
from user.models import Profile


class ProfileFrom(forms.ModelForm):

    def clean_max_diatance(self):
        # 以下函数是为了防止恶意操作对比最小公里数是小于最大公里数的,有些人将最大公里数调为6,
        # 而最小公里数为8,为了避免这个问题,有以下代码
        max_diatance = self.cleaned_data.get('max_diatance')
        min_diatance = self.cleaned_data.get('min_diatance')

        if max_diatance < min_diatance:
            raise forms.ValidationError('最大匹配公里数必须大于最小匹配的距离')
        return max_diatance

    def clean_max_dating_age(self):
        max_dating_age = self.cleaned_data.get('max_dating_age')
        min_dating_age = self.cleaned_data.get('min_dating_age')

        if max_dating_age < min_dating_age:
            raise forms.ValidationError('最大匹配年龄必须大于最小匹配的年龄')
        return max_dating_age






    class Meta:
        model = Profile
        fields = ['location',
                  'min_diatance',
                  'max_diatance',
                  'min_dating_age',
                  'max_dating_age',
                  'dating_sex']
        # fields = '__all__'   这一个是可以提取所有,但是我们现在auto-play,不需要,所为我们不用这个