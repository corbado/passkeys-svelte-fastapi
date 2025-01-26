<script lang="ts">
	import Corbado from '@corbado/web-js';
	import userStore from '../../stores/user.svelte';

	type SecretStatus =
		| { status: 'idle' }
		| { status: 'loading' }
		| { status: 'success'; secret: string }
		| { status: 'error'; error: string };

	let isAuthenticated = $derived(
		userStore.userInfo.status === 'authenticated'
	);
	let revealSecretResult = $state<SecretStatus>({ status: 'idle' });

	async function fetchSecret() {
		revealSecretResult.status = 'loading';
		const secretGetUrl = `${import.meta.env.VITE_BACKEND_BASE_URL}/api/secret`;
		try {
			const rsp = await fetch(secretGetUrl, {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${Corbado.sessionToken}`
				}
			});
			if (!rsp.ok)
				throw new Error(`Failed to get secret: ${rsp.statusText}`);
			const json = (await rsp.json()) as { secret: string };
			revealSecretResult = { status: 'success', secret: json.secret };
		} catch (e) {
			revealSecretResult = { status: 'error', error: `${e}` };
		}
	}
</script>

{#if isAuthenticated}
	<h1>User area!</h1>
	<p>Since you are logged-in, we can tell you a secret:</p>
	<button
		id="reveal-secret-button"
		onclick={fetchSecret}
		disabled={['loading', 'success'].includes(revealSecretResult.status)}
	>
		Reveal secret
	</button>
	<div id="reveal-secret-result">
		{#if revealSecretResult.status === 'success'}
			<div id="secret-box">
				<h3>Secret:</h3>
				<p>{revealSecretResult.secret}</p>
			</div>
		{:else if revealSecretResult.status === 'loading'}
			<div class="loader"></div>
		{:else if revealSecretResult.status === 'error'}
			<p>Failed to reveal secret: {revealSecretResult.error}</p>
		{/if}
	</div>
{:else}
	<h1>User area!</h1>
	<p>This page is for logged-in users only. Please login:</p>
	<a class="button" href="/login">Login</a>
{/if}
