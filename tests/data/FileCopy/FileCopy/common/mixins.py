# Желательно придерживаться единой реализации данного модуля 
# для всех действий файловой системы

from typing import Any, Optional, Mapping


class InOutMixin:
    """Класс, использующий данный миксин, должен содержать следующие аттрибуты класса:
    
    # Маппинг входных параметров
    Parameters = dict(
        <имя аттрибута DTO>=(<флаг обязательноко аттрибута|bool>, <класс/конструктор аттрибута|type>),
        ...
    )

    # Маппинг значений по умолчанию
    Defaults = dict(
        <имя аттрибута DTO>=<нативное значение Python>,
        ...
    )

    # Маппинг результатов
    Results = dict(
        <имя аттрибута DTO>=<класс/конструктор аттрибута|type>
    )

    """
    def get_params(self) -> Mapping[str, Any]:
        """Get params as native Python types, fill defaults if any
        """
        def unwrap_value(d: Any) -> Any:
            """Приведение данных к нативному типу Python"""
            try:
                # Извлечь значение из не-нативного (DTO) объекта:
                return d.get_valueOf_()
            except AttributeError:
                # Это нативный тип Python:
                return d
        params = { 
            name: unwrap_value(self.parameters.get(name)) \
            for name in self.Parameters.keys() \
                if self.parameters.get(name) is not None}
        
        # Применить дефолтные значения к пропущенным:
        kwargs = self.Defaults.copy()
        kwargs.update(params)
        return kwargs


    def set_result_attribute(self, 
            result_dict: Mapping[str, Any], 
            attr_name: str, 
            value: Any) -> None:

        result_type = self.Results[attr_name]
        if hasattr(result_type, 'set_valueOf_'):
            wrapper_object = result_type()
            wrapper_object.set_valueOf_(value)
            value = wrapper_object

        result_dict[attr_name] = value


    def implements_scalar_result(self):
        "Действие должно возвращать единственное значение"
        return len(self.Results.keys()) < 2