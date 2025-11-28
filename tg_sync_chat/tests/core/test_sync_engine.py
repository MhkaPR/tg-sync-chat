import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from core.sync_engine import SyncEngine


class TestSyncEngine:
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock dependencies for SyncEngine"""
        mock_mapper = Mock()
        mock_truth_repo = Mock()
        mock_telegram_repo = Mock()
        mock_recognizer = Mock()
        mock_sync_worker = Mock()
        
        return {
            'mapper': mock_mapper,
            'truth_repo': mock_truth_repo,
            'telegram_repo': mock_telegram_repo,
            'recognizer': mock_recognizer,
            'sync_worker': mock_sync_worker
        }
    
    @pytest.fixture
    def sync_engine(self, mock_dependencies):
        """Create SyncEngine instance with mock dependencies"""
        engine = SyncEngine(
            mapper=mock_dependencies['mapper'],
            truth_repo=mock_dependencies['truth_repo'],
            telegram_repo=mock_dependencies['telegram_repo'],
            recognizer=mock_dependencies['recognizer'],
            sync_worker=mock_dependencies['sync_worker'],
            duration=0.1  # Shorter duration for tests
        )
        # Add common ignored exceptions for tests
        engine._ignored_exceptions = [Exception]
        return engine

    @pytest.fixture(autouse=True)
    def mock_sleep(self):
        """Automatically mock asyncio.sleep for all tests"""
        with patch('core.sync_engine.sleep', AsyncMock()) as mock_sleep:
            yield mock_sleep

    @pytest.mark.asyncio
    async def test_run_without_deletables(self, sync_engine, mock_dependencies, mock_sleep):
        """Test run method without deletables"""
        # Mock recognizer methods
        mock_dependencies['recognizer'].find_creatables = AsyncMock(return_value=['item1', 'item2'])
        mock_dependencies['recognizer'].find_updatables = AsyncMock(return_value=['item3'])
        mock_dependencies['recognizer'].find_deletables = AsyncMock(return_value=[])
        
        # Mock sync worker methods
        mock_dependencies['sync_worker'].load_available_changes = Mock()
        mock_dependencies['sync_worker'].synchronize = Mock()
        
        # Configure sleep to stop after first iteration
        async def stop_after_first_call(duration):
            mock_sleep.return_value = None
            sync_engine._stop = True
        
        mock_sleep.side_effect = stop_after_first_call
        
        await sync_engine.run(also_deletables=False)
        
        # Verify recognizer was called exactly once
        mock_dependencies['recognizer'].find_creatables.assert_called_once()
        mock_dependencies['recognizer'].find_updatables.assert_called_once()
        mock_dependencies['recognizer'].find_deletables.assert_not_called()
        
        # Verify sync worker was called with correct parameters
        mock_dependencies['sync_worker'].load_available_changes.assert_called_once_with(
            creatables=['item1', 'item2'],
            updatables=['item3'],
            deletables=[]
        )
        mock_dependencies['sync_worker'].synchronize.assert_called_once_with(also_deletables=False)
        mock_sleep.assert_called_once_with(0.1)

    @pytest.mark.asyncio
    async def test_run_with_deletables(self, sync_engine, mock_dependencies, mock_sleep):
        """Test run method with deletables"""
        # Mock recognizer methods
        mock_dependencies['recognizer'].find_creatables = AsyncMock(return_value=['item1'])
        mock_dependencies['recognizer'].find_updatables = AsyncMock(return_value=[])
        mock_dependencies['recognizer'].find_deletables = AsyncMock(return_value=['item4'])
        
        # Mock sync worker methods
        mock_dependencies['sync_worker'].load_available_changes = Mock()
        mock_dependencies['sync_worker'].synchronize = Mock()
        
        # Configure sleep to stop after first iteration
        async def stop_after_first_call(duration):
            mock_sleep.return_value = None
            sync_engine._stop = True
        
        mock_sleep.side_effect = stop_after_first_call
        
        await sync_engine.run(also_deletables=True)
        
        # Verify recognizer was called exactly once
        mock_dependencies['recognizer'].find_creatables.assert_called_once()
        mock_dependencies['recognizer'].find_updatables.assert_called_once()
        mock_dependencies['recognizer'].find_deletables.assert_called_once()
        
        # Verify sync worker was called with correct parameters
        mock_dependencies['sync_worker'].load_available_changes.assert_called_once_with(
            creatables=['item1'],
            updatables=[],
            deletables=['item4']
        )
        mock_dependencies['sync_worker'].synchronize.assert_called_once_with(also_deletables=True)
        mock_sleep.assert_called_once_with(0.1)

    @pytest.mark.asyncio
    async def test_run_multiple_iterations(self, sync_engine, mock_dependencies, mock_sleep):
        """Test that run method executes multiple iterations"""
        # Mock recognizer methods to return different values each call
        creatables_mock = AsyncMock(side_effect=[['item1'], ['item2'], ['item3']])
        updatables_mock = AsyncMock(side_effect=[['itemA'], ['itemB'], []])
        deletables_mock = AsyncMock(return_value=[])
        
        mock_dependencies['recognizer'].find_creatables = creatables_mock
        mock_dependencies['recognizer'].find_updatables = updatables_mock
        mock_dependencies['recognizer'].find_deletables = deletables_mock
        
        # Mock sync worker methods
        mock_dependencies['sync_worker'].load_available_changes = Mock()
        mock_dependencies['sync_worker'].synchronize = Mock()
        
        # Configure sleep to count iterations and stop after 3
        call_count = 0
        async def stop_after_three_calls(duration):
            nonlocal call_count
            call_count += 1
            if call_count >= 3:
                sync_engine._stop = True
        
        mock_sleep.side_effect = stop_after_three_calls
        
        await sync_engine.run(also_deletables=False)
        
        # Verify multiple calls were made
        assert mock_dependencies['recognizer'].find_creatables.call_count == 3
        assert mock_dependencies['recognizer'].find_updatables.call_count == 3
        assert mock_dependencies['sync_worker'].load_available_changes.call_count == 3
        assert mock_dependencies['sync_worker'].synchronize.call_count == 3
        assert mock_sleep.call_count == 3
        assert all(call[0][0] == 0.1 for call in mock_sleep.call_args_list)

    @pytest.mark.asyncio
    async def test_run_with_exception(self, sync_engine, mock_dependencies, mock_sleep):
        """Test that run method continues after exception"""
        # Mock recognizer to raise exception on first call, then work normally

        creatables_mock = AsyncMock(side_effect=[
            Exception("Test error"),
            ['item1'],
            ['item2']
        ])
        updatables_mock = AsyncMock(side_effect=[
            ['itemA'],
            []
        ])
        
        mock_dependencies['recognizer'].find_creatables = creatables_mock
        mock_dependencies['recognizer'].find_updatables = updatables_mock
        mock_dependencies['recognizer'].find_deletables = AsyncMock(return_value=[])
        
        # Mock sync worker methods
        mock_dependencies['sync_worker'].load_available_changes = Mock()
        mock_dependencies['sync_worker'].synchronize = Mock()
        
        # Configure sleep to stop after 2 successful iterations
        successful_iterations = 0
        async def stop_after_two_successful(duration):
            nonlocal successful_iterations
            # Count only iterations that don't raise exceptions
            if mock_dependencies['recognizer'].find_creatables.call_count >= 2:  # After first exception
                successful_iterations += 1
            if successful_iterations >= 2:
                sync_engine._stop = True
        
        mock_sleep.side_effect = stop_after_two_successful
        
        await sync_engine.run(also_deletables=False)
        
        # Should have attempted multiple calls despite exceptions
        assert mock_dependencies['recognizer'].find_creatables.call_count == 3  # 1 fail + 2 success
        assert mock_dependencies['recognizer'].find_updatables.call_count == 2  # 1 fail + 2 success
        
        # Sync worker should have been called for successful iterations only
        assert mock_dependencies['sync_worker'].load_available_changes.call_count == 2
        assert mock_dependencies['sync_worker'].synchronize.call_count == 2
        assert mock_sleep.call_count >= 2

    @pytest.mark.asyncio
    async def test_stop_method(self, sync_engine):
        """Test that stop method sets _stop flag"""
        sync_engine._stop = False
        await sync_engine.stop()
        assert sync_engine._stop is True

    @pytest.mark.asyncio
    async def test_run_respects_stop_flag(self, sync_engine, mock_dependencies, mock_sleep):
        """Test that run method stops when _stop flag is set"""
        # Mock recognizer methods
        mock_dependencies['recognizer'].find_creatables = AsyncMock(return_value=[])
        mock_dependencies['recognizer'].find_updatables = AsyncMock(return_value=[])
        mock_dependencies['recognizer'].find_deletables = AsyncMock(return_value=[])
        
        # Mock sync worker methods
        mock_dependencies['sync_worker'].load_available_changes = Mock()
        mock_dependencies['sync_worker'].synchronize = Mock()
        
        # Set stop flag immediately
        sync_engine._stop = True
        
        await sync_engine.run(also_deletables=False)
        
        # Verify no calls were made since we stopped immediately
        mock_dependencies['recognizer'].find_creatables.assert_not_called()
        mock_dependencies['recognizer'].find_updatables.assert_not_called()
        mock_dependencies['sync_worker'].load_available_changes.assert_not_called()
        mock_dependencies['sync_worker'].synchronize.assert_not_called()
        mock_sleep.assert_not_called()

    def test_init_with_custom_dependencies(self, mock_dependencies):
        """Test initialization with custom dependencies"""
        engine = SyncEngine(
            mapper=mock_dependencies['mapper'],
            truth_repo=mock_dependencies['truth_repo'],
            telegram_repo=mock_dependencies['telegram_repo'],
            recognizer=mock_dependencies['recognizer'],
            sync_worker=mock_dependencies['sync_worker'],
            duration=5
        )
        
        assert engine.mapper == mock_dependencies['mapper']
        assert engine.truth_repo == mock_dependencies['truth_repo']
        assert engine.telegram_repo == mock_dependencies['telegram_repo']
        assert engine.recognizer == mock_dependencies['recognizer']
        assert engine.sync_worker == mock_dependencies['sync_worker']
        assert engine._duration == 5
        assert engine._stop is False

    def test_init_with_default_dependencies(self):
        """Test initialization with default dependencies"""
        mock_bot = Mock()
        engine = SyncEngine(bot=mock_bot, channel_id="test_channel")
        
        from core.mapper import Mapper
        from infrastructures.repositories.mem_truth_repo import MemoryTruthRepo
        from infrastructures.repositories.aiogram import AiogramMemoryRepo
        from core.recognizer import Recognizer
        from core.sync_worker import SyncWorker
        
        assert isinstance(engine.mapper, Mapper)
        assert isinstance(engine.truth_repo, MemoryTruthRepo)
        assert isinstance(engine.telegram_repo, AiogramMemoryRepo)
        assert isinstance(engine.recognizer, Recognizer)
        assert isinstance(engine.sync_worker, SyncWorker)
        assert engine._duration == 1
        assert engine._stop is False

    def test_init_missing_kwargs_for_default_telegram_repo(self):
        """Test that initialization fails when kwargs are missing for default telegram repo"""
        with pytest.raises(KeyError):
            SyncEngine()  # Missing bot and channel_id

    @pytest.mark.asyncio
    async def test_run_with_custom_ignored_exceptions(self, mock_dependencies, mock_sleep):
        """Test that run method respects custom ignored exceptions"""
        # Create engine with custom ignored exceptions
        engine = SyncEngine(
            mapper=mock_dependencies['mapper'],
            truth_repo=mock_dependencies['truth_repo'],
            telegram_repo=mock_dependencies['telegram_repo'],
            recognizer=mock_dependencies['recognizer'],
            sync_worker=mock_dependencies['sync_worker'],
            duration=0.1,
            ignored_exceptions=[ValueError, TypeError]
        )
        
        # Mock recognizer to raise a ValueError (which should be ignored)
        mock_dependencies['recognizer'].find_creatables = AsyncMock(side_effect=ValueError("Test"))
        mock_dependencies['recognizer'].find_updatables = AsyncMock(return_value=[])
        mock_dependencies['recognizer'].find_deletables = AsyncMock(return_value=[])
        
        # Mock sync worker methods
        mock_dependencies['sync_worker'].load_available_changes = Mock()
        mock_dependencies['sync_worker'].synchronize = Mock()
        
        # Configure sleep to stop after first iteration
        async def stop_after_first_call(duration):
            engine._stop = True
        
        mock_sleep.side_effect = stop_after_first_call
        
        # Should not raise ValueError since it's in ignored_exceptions
        await engine.run(also_deletables=False)
        
        # Verify calls were attempted but sync worker wasn't called due to exception
        mock_dependencies['recognizer'].find_creatables.assert_called_once()
        mock_dependencies['sync_worker'].load_available_changes.assert_not_called()