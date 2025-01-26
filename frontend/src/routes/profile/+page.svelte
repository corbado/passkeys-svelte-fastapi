<script lang="ts">
	import Corbado from '@corbado/web-js';
	import { goto } from '$app/navigation';
	import userStore from '../../stores/user.svelte';

	let passkeyListDiv: HTMLDivElement;

	$effect(() => {
		if (userStore.userInfo.status === 'not-authenticated') {
			goto('/login');
			return;
		}
	});
	userStore.onCorbadoLoaded(() => {
		Corbado.mountPasskeyListUI(passkeyListDiv);
	});

	let externalUserInfo = $derived(
		userStore.externalUserInfo.status === 'success'
			? userStore.externalUserInfo
			: null
	);
</script>

<h1>Profile</h1>
<p><strong>Example userID: </strong>{externalUserInfo?.user.id}</p>
<!-- We could also get this id from the Corbado web-js package instead of our backend -->
<p>
	<strong>Corbado userID: </strong>{externalUserInfo?.user.corbado_user_id}
</p>
<h2>Your Identifiers</h2>
{#if externalUserInfo}
	<div id="identifier-list">
		{#each externalUserInfo.identifiers as identifier (identifier.identifierID)}
			<div>
				<p><strong>Type:</strong> {identifier.type}</p>
				<p><strong>Value:</strong> {identifier.value}</p>
			</div>
		{/each}
	</div>
{/if}
<h2>Manage your Passkeys</h2>
<div bind:this={passkeyListDiv}></div>
