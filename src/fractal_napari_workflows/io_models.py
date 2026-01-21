from typing import Literal, Optional, Self

from fractal_tasks_core.channels import ChannelInputModel
from pydantic import BaseModel, model_validator


class NapariWorkflowsOutput(BaseModel):
    """A value of the `output_specs` argument in `napari_workflows_wrapper`.

    Attributes:
        type: Output type (either `label` or `dataframe`).
        label_name: Label name (for label outputs, it is used as the name of
            the label; for dataframe outputs, it is used to fill the
            `region["path"]` field).
        table_name: Table name (for dataframe outputs only).
    """

    type: Literal["label", "dataframe"]
    label_name: str
    table_name: Optional[str] = None

    @model_validator(mode="after")
    def table_name_only_for_dataframe_type(self: Self) -> Self:
        """Check that table_name is set only for dataframe outputs."""
        _type = self.type
        _table_name = self.table_name
        if (_type == "dataframe" and (not _table_name)) or (
            _type != "dataframe" and _table_name
        ):
            raise ValueError(
                f"Output item has type={_type} but table_name={_table_name}."
            )
        return self


class NapariWorkflowsInput(BaseModel):
    """A value of the `input_specs` argument in `napari_workflows_wrapper`.

    Attributes:
        type: Input type (either `image` or `label`).
        label_name: Label name (for label inputs only).
        channel: `ChannelInputModel` object (for image inputs only).
    """

    type: Literal["image", "label"]
    label_name: Optional[str] = None
    channel: Optional[ChannelInputModel] = None

    @model_validator(mode="after")
    def label_name_is_present(self: Self) -> Self:
        """Check that label inputs have `label_name` set."""
        label_name = self.label_name
        _type = self.type
        if _type == "label" and label_name is None:
            raise ValueError(
                f"Input item has type={_type} but label_name={label_name}."
            )
        return self

    @model_validator(mode="after")
    def channel_is_present(self: Self) -> Self:
        """Check that image inputs have `channel` set."""
        _type = self.type
        channel = self.channel
        if _type == "image" and channel is None:
            raise ValueError(f"Input item has type={_type} but channel={channel}.")
        return self
