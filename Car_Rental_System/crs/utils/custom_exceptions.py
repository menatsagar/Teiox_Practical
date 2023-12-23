from dataclasses import dataclass


@dataclass(frozen=True)
class UserRegistrationException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class UserAlreadyExistsException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class UserLoginException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class UserLogoutException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class VehicleCreationException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class VehicleEditException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class DeleteVehicleException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class VehicleCreationException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class EditVehicleException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class DeleteVehicleException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class BookingCreationException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class EditBookingException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"


@dataclass(frozen=True)
class DeleteBookingException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"
    
@dataclass(frozen=True)
class BookingAlreadyExistsException(Exception):
    item: str
    message: str

    def exception_dict(self) -> dict:
        return {"item": self.item, "message": self.message}

    def __repr__(self):
        return f"{self.item}: {self.message}"
