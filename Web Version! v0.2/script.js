let intervalId = null; // Variabel global untuk menyimpan ID interval

function showCalculator() {
    document.getElementById('calculator').classList.remove('hidden');
    document.getElementById('tutorial').classList.add('hidden');
}

function showTutorial() {
    document.getElementById('tutorial').classList.remove('hidden');
    document.getElementById('calculator').classList.add('hidden');
}

function showAbout() {
    Swal.fire({
        title: 'Tentang',
        html: `
            <p><strong>SweetAlert2</strong>: v11.7.0</p>
            <p><strong>Bootstrap</strong>: v5.3.0</p>
            <p>Program ini menghitung sisa waktu dan penggunaan kuota internet berdasarkan input yang diberikan.</p>
        `,
        icon: 'info',
        confirmButtonText: 'Tutup'
    });
}

function startCountdown() {
    if (intervalId !== null) {
        // Jika intervalId tidak null, berarti interval sudah ada
        Swal.fire({
            icon: 'warning',
            title: 'Perhatian',
            text: 'Hitung mundur sedang berjalan!',
        });
        return;
    }

    const datetimeInput = document.getElementById('datetime').value;
    const quotaInput = parseFloat(document.getElementById('quota').value);

    if (!datetimeInput || isNaN(quotaInput) || quotaInput <= 0) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Masukkan tanggal, waktu, dan total kuota yang valid!',
        });
        return;
    }

    const targetDatetime = new Date(datetimeInput.replace('T', ' '));
    const totalQuota = quotaInput;

    const output = document.getElementById('output');
    const startTime = new Date();

    intervalId = setInterval(() => {
        const now = new Date();
        const remainingTime = targetDatetime - now;

        if (remainingTime <= 0) {
            clearInterval(intervalId);
            intervalId = null; // Reset intervalId saat interval selesai
            output.innerHTML = "<div class='alert alert-danger'>Waktu habis!</div>";
            return;
        }

        const days = Math.floor(remainingTime / (24 * 60 * 60 * 1000));
        const hours = Math.floor((remainingTime % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000));
        const minutes = Math.floor((remainingTime % (60 * 60 * 1000)) / (60 * 1000));
        const seconds = Math.floor((remainingTime % (60 * 1000)) / 1000);

        const elapsedSeconds = (now - startTime) / 1000;
        const totalSeconds = (targetDatetime - startTime) / 1000;
        const quotaPerSecond = totalQuota / totalSeconds;
        const usedQuota = elapsedSeconds * quotaPerSecond;

        const formattedUsedQuota = formatSize(Math.min(usedQuota, totalQuota));
        const formattedTotalQuota = formatSize(totalQuota);

        let formattedUsage;
        if (totalSeconds > 3600) { // Lebih dari 1 jam
            const quotaPerMinute = quotaPerSecond * 60;
            const quotaPerHour = quotaPerMinute * 60;
            formattedUsage = `${formatSize(quotaPerMinute)}/mnt (${formatSize(quotaPerHour)}/jam)`;
        } else if (totalSeconds > 60) { // Lebih dari 1 menit
            const quotaPerMinute = quotaPerSecond * 60;
            formattedUsage = `${formatSize(quotaPerSecond)}/s (${formatSize(quotaPerMinute)}/mnt)`;
        } else { // Kurang dari 1 menit
            formattedUsage = `${formatSize(quotaPerSecond)}/s`;
        }

        output.innerHTML = `<div class='alert alert-info'>Waktu mundur: ${String(days).padStart(2, '0')}:${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')} | Kuota: ${formattedUsedQuota}/${formattedTotalQuota} | ${formattedUsage}</div>`;
    }, 1000);
}

function formatSize(sizeInMb) {
    if (sizeInMb >= 1024) {
        const sizeInGb = sizeInMb / 1024;
        return `${sizeInGb.toFixed(2)}GB`;
    } else if (sizeInMb >= 1) {
        return `${sizeInMb.toFixed(2)}MB`;
    } else {
        const sizeInKb = sizeInMb * 1024;
        return `${sizeInKb.toFixed(2)}KB`;
    }
}
