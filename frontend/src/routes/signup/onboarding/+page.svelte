<script lang="ts">
	import { goto } from '$app/navigation';
	import userStore from '../../../stores/user.svelte';

	$effect(() => {
		if (userStore.userInfo.status === 'not-authenticated') {
			goto('/login');
		}
	});

	async function onSubmit(event: Event) {
		event.preventDefault();

		const form = event.target as HTMLFormElement;
		const formData = new FormData(form);
		const city = formData.get('city') as string;
		try {
			await userStore.updateUserCity(city);
		} catch (e) {
			console.error('Failed to update user city:', e);
		}
		await goto('/');
	}
</script>

<h1>Onboarding</h1>
<h2>Choose your city</h2>
<form id="city-form" method="post" onsubmit={onSubmit}>
	<input type="text" name="city" required />
	<button type="submit">Finish onboarding</button>
</form>
