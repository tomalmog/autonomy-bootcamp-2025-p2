"""
Heartbeat receiving logic.
"""

from pymavlink import mavutil

from ..common.modules.logger import logger


# =================================================================================================
#                            ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# =================================================================================================
class HeartbeatReceiver:
    """
    HeartbeatReceiver class to send a heartbeat
    """

    __private_key = object()

    @classmethod
    def create(
        cls,
        connection: mavutil.mavfile,
        heartbeat_period_s: float,
        local_logger: logger.Logger,
    ) -> "tuple[bool, HeartbeatReceiver | None]":
        """
        Falliable create (instantiation) method to create a HeartbeatReceiver object.
        """
        try:
            return True, HeartbeatReceiver(
                HeartbeatReceiver.__private_key,
                connection,
                heartbeat_period_s,
            )
        except:  # pylint: disable=bare-except
            local_logger.error("Failed to create HeartbeatReceiver", True)
            return False, None

    def __init__(
        self,
        key: object,
        connection: mavutil.mavfile,
        heartbeat_period_s: float,
    ) -> None:
        assert key is HeartbeatReceiver.__private_key, "Use create() method"

        # Do any intializiation here
        self.__connection = connection
        self.__period_s = heartbeat_period_s

    def run(
        self,
        disconnect_threshold: int,
        local_logger: logger.Logger,
    ) -> "tuple[bool, str, int]":
        """
        Attempt to recieve a heartbeat message.
        If disconnected for over a threshold number of periods,
        the connection is considered disconnected.
        """
        try:
            msg = self.__connection.recv_match(
                type="HEARTBEAT", blocking=True, timeout=self.__period_s
            )
        except Exception as e:  # pylint: disable=broad-except
            local_logger.error(f"Exception while receiving heartbeat: {e}", True)
            msg = None

        missed = 0
        state = "Connected"
        if not msg or msg.get_type() != "HEARTBEAT":
            missed = 1
            local_logger.warning("Missed heartbeat", True)
        if missed >= disconnect_threshold:
            state = "Disconnected"
        return True, state, missed


# =================================================================================================
#                            ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# =================================================================================================
